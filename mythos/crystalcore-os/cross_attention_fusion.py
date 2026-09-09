# CrystalCore.OS - Cross-Attention Fusion for Multimodal Emotion Detection
# Enables text, audio, and visual modalities to attend to each other's features

import logging
from typing import Optional, Tuple, Dict

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)


class CrossAttentionFusion(nn.Module):
    """Multi-head cross-attention fusion for combining modalities."""

    def __init__(
        self,
        text_dim: int = 768,
        audio_dim: int = 768,
        vision_dim: int = 512,
        hidden_dim: int = 512,
        num_heads: int = 8,
        dropout: float = 0.1,
    ):
        """
        Initialize cross-attention fusion module.

        Args:
            text_dim: Text embedding dimension (DistilBERT: 768)
            audio_dim: Audio embedding dimension (HuBERT: 768)
            vision_dim: Vision embedding dimension (ViT: 512)
            hidden_dim: Hidden dimension for projection
            num_heads: Number of attention heads
            dropout: Dropout rate
        """
        super().__init__()

        self.text_proj = nn.Linear(text_dim, hidden_dim)
        self.audio_proj = nn.Linear(audio_dim, hidden_dim)
        self.vision_proj = nn.Linear(vision_dim, hidden_dim)

        # Multi-head attention for cross-modal interaction
        self.cross_attn_text_audio = nn.MultiheadAttention(
            hidden_dim, num_heads=num_heads, batch_first=True, dropout=dropout
        )
        self.cross_attn_text_vision = nn.MultiheadAttention(
            hidden_dim, num_heads=num_heads, batch_first=True, dropout=dropout
        )

        # Fusion network
        self.fusion_net = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 28),  # 28 emotion classes
        )

        logger.info(
            f"CrossAttentionFusion initialized: "
            f"text_dim={text_dim}, audio_dim={audio_dim}, vision_dim={vision_dim}"
        )

    def forward(
        self,
        text_features: torch.Tensor,
        audio_features: Optional[torch.Tensor] = None,
        vision_features: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Forward pass through cross-attention fusion.

        Args:
            text_features: [batch_size, text_dim]
            audio_features: [batch_size, audio_dim] (optional)
            vision_features: [batch_size, vision_dim] (optional)

        Returns:
            logits: [batch_size, 28] emotion classification logits
        """
        batch_size = text_features.shape[0]

        # Project to common dimension
        t = self.text_proj(text_features).unsqueeze(1)  # [batch, 1, hidden]
        fused_features = [t]

        # Text-Audio cross-attention
        if audio_features is not None:
            a = self.audio_proj(audio_features).unsqueeze(1)  # [batch, 1, hidden]
            attn_out, _ = self.cross_attn_text_audio(t, a, a)  # Query: text, Key/Value: audio
            fused_features.append(attn_out)

        # Text-Vision cross-attention
        if vision_features is not None:
            v = self.vision_proj(vision_features).unsqueeze(1)  # [batch, 1, hidden]
            attn_out, _ = self.cross_attn_text_vision(t, v, v)  # Query: text, Key/Value: vision
            fused_features.append(attn_out)

        # Concatenate all features
        if len(fused_features) > 1:
            fused = torch.cat(fused_features, dim=1)  # [batch, num_modalities, hidden]
            fused = fused.mean(dim=1)  # [batch, hidden] - average pooling
        else:
            fused = t.squeeze(1)  # [batch, hidden] - text only

        # Ensure correct shape for fusion network
        if fused.dim() == 1:
            fused = fused.unsqueeze(0)

        # Pad or concatenate to expected fusion input size (hidden_dim * 3)
        if len(fused_features) == 1:  # Text only
            fused = torch.cat(
                [fused, torch.zeros_like(fused), torch.zeros_like(fused)], dim=1
            )
        elif len(fused_features) == 2:  # Text + one modality
            fused = torch.cat(
                [fused, fused[:, : fused.shape[1] // 2], torch.zeros_like(fused[:, : fused.shape[1] // 2])],
                dim=1,
            )

        # Final emotion classification
        logits = self.fusion_net(fused)

        return logits


class MultimodalEmotionDetector:
    """Complete multimodal emotion detector with cross-attention fusion."""

    def __init__(
        self,
        model_dir: str = "./crystalcore_emotion_model",
        fusion_hidden_dim: int = 512,
    ):
        """Initialize multimodal detector."""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification

            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            self.text_model = AutoModelForSequenceClassification.from_pretrained(
                model_dir, num_labels=28
            )
        except Exception as e:
            logger.warning(f"Could not load pretrained model: {e}")
            self.text_model = None

        self.fusion_model = CrossAttentionFusion(hidden_dim=fusion_hidden_dim)
        logger.info("MultimodalEmotionDetector initialized with cross-attention fusion")

    def detect_emotion(
        self,
        text: str,
        audio_features: Optional[torch.Tensor] = None,
        vision_features: Optional[torch.Tensor] = None,
    ) -> Dict:
        """
        Detect emotion using cross-attention fusion.

        Args:
            text: Input text
            audio_features: Audio embeddings (optional)
            vision_features: Vision embeddings (optional)

        Returns:
            Dictionary with emotion, confidence, modalities used
        """
        # Extract text features
        if self.text_model is not None:
            inputs = self.tokenizer(
                text, return_tensors="pt", padding=True, truncation=True, max_length=128
            )
            with torch.no_grad():
                outputs = self.text_model.base_model(**inputs)
                text_emb = outputs.last_hidden_state.mean(dim=1)  # [1, 768]
        else:
            # Fallback: use text embedding from tokenizer
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            text_emb = torch.randn(1, 768)  # Random for testing
            logger.warning("Using random text embedding (model not loaded)")

        # Forward through fusion model
        with torch.no_grad():
            logits = self.fusion_model(text_emb, audio_features, vision_features)
            probs = F.softmax(logits, dim=1)
            confidence, emotion_idx = torch.max(probs, dim=1)

        from .huggingface_trainer import EMOTION_LABEL_MAP

        emotion = EMOTION_LABEL_MAP.get(emotion_idx.item(), "neutral")
        modalities = ["text"]
        if audio_features is not None:
            modalities.append("audio")
        if vision_features is not None:
            modalities.append("vision")

        return {
            "emotion": emotion,
            "emotion_idx": emotion_idx.item(),
            "confidence": round(confidence.item(), 4),
            "modalities": modalities,
            "logits": logits,
        }


def visualize_fusion_architecture() -> str:
    """Return ASCII visualization of cross-attention fusion architecture."""
    return """
    ╔════════════════════════════════════════════════════════════╗
    ║         CrystalCore.OS Cross-Attention Fusion              ║
    ╠════════════════════════════════════════════════════════════╣
    ║                                                            ║
    ║  TEXT BRANCH          AUDIO BRANCH        VISION BRANCH   ║
    ║  ┌──────────┐         ┌──────────┐        ┌──────────┐   ║
    ║  │DistilBRT│         │ HuBERT   │        │ ViT/CLIP │   ║
    ║  └────┬─────┘         └────┬─────┘        └────┬─────┘   ║
    ║       │                    │                   │          ║
    ║       ├─────┐────────────┬─┴─┐───────────┬─────┤          ║
    ║       ▼     ▼            ▼   ▼           ▼     ▼          ║
    ║   [Project to Hidden Dim]                                 ║
    ║       t = Proj(text)    a = Proj(audio)  v = Proj(vision)║
    ║                                                            ║
    ║        ┌─────────────────────────────────────────┐        ║
    ║        │   Cross-Attention Layers               │        ║
    ║        │  (Text queries Audio & Vision keys)    │        ║
    ║        └─────────┬──────────────────────────────┘        ║
    ║                  │                                        ║
    ║        ┌─────────▼──────────────────────────────┐        ║
    ║        │  Concatenate & Mean Pooling           │        ║
    ║        │  [t ⊕ attn(t,a) ⊕ attn(t,v)]         │        ║
    ║        └─────────┬──────────────────────────────┘        ║
    ║                  │                                        ║
    ║        ┌─────────▼──────────────────────────────┐        ║
    ║        │  Fusion Network (ReLU layers)         │        ║
    ║        │  hidden_dim*3 → 28 emotion classes    │        ║
    ║        └─────────┬──────────────────────────────┘        ║
    ║                  │                                        ║
    ║        ┌─────────▼──────────────────────────────┐        ║
    ║        │  Output Logits + Softmax              │        ║
    ║        │  [admiration, amusement, ..., neutral]│        ║
    ║        └────────────────────────────────────────┘        ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝

    Key Innovation:
    - Text attends to Audio & Vision modalities
    - Each modality contributes to final emotion prediction
    - Late fusion: information flows through attention heads
    - Scalable: add more modalities easily
    """
