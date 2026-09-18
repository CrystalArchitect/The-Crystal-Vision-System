// SPDX-License-Identifier: MIT

import React, { useState } from 'react';
import { Heart } from 'lucide-react';
import { useUserStore } from '../../lib/userStore';
import LoginPrompt from './LoginPrompt';

interface FavoritesButtonProps {
  trackId: string;
  isFavorited?: boolean;
  onToggle?: (trackId: string, isFavorited: boolean) => void;
  size?: number;
}

export default function FavoritesButton({
  trackId,
  isFavorited = false,
  onToggle,
  size = 20,
}: FavoritesButtonProps) {
  const { currentUser } = useUserStore();
  const [favorited, setFavorited] = useState(isFavorited);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  const handleToggle = () => {
    if (!currentUser) {
      setShowLoginPrompt(true);
      return;
    }

    const newState = !favorited;
    setFavorited(newState);
    onToggle?.(trackId, newState);
  };

  return (
    <>
      <button
        onClick={handleToggle}
        className="p-2 hover:opacity-75 transition-opacity"
        aria-label={favorited ? 'Remove from favorites' : 'Add to favorites'}
      >
        <Heart
          size={size}
          className={favorited ? 'fill-accent text-accent' : 'text-gray-400 dark:text-gray-600'}
        />
      </button>
      {showLoginPrompt && (
        <LoginPrompt feature="save favorites" onClose={() => setShowLoginPrompt(false)} />
      )}
    </>
  );
}
