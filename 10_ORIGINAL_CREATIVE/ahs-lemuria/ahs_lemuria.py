#!/usr/bin/env python3
"""Project American Horror Story: Lemuria — terminal sandbox.

Canon: no · Layer: vision / story · Fan fiction inspired by anthology form.
Not affiliated with or endorsed by FX / American Horror Story.
Celestial Portal framing is narrative only unless wired to a live gateway.
"""

from __future__ import annotations

import random
import sys


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"[SYSTEM LOG]: {title}")
    print("=" * 60)


def boot_portal() -> None:
    print_header("CELESTIAL PORTAL ONLINE")
    print("Initializing subspace frequencies...")
    print("Establishing connection to deep-trench historical archives...")
    print("Project American Horror Story: Lemuria is now executing.")
    print()
    print("[SYSTEM LOG]")
    print("STATUS: Active")
    print("LOCATION: Displaced Coordinates, Pacific Basin / Sub-Oceanic Crypt")
    print("OBJECTIVE: Unearth the Sunken Colony of Lemuria")
    print("CODENAME: The Devouring Deep")


def start_game() -> None:
    metrics = {"integrity": 100, "psychosis": 0, "wake": 0}
    phase = 1

    boot_portal()
    print_header("PROJECT_AHS_LEMURIA // ABSOLUTE DEEP-SEA HORROR SIMULATOR")
    print("Aegir Station has breached the abyssal shelf at 11,000m beneath the Pacific.")
    print("The extraction drill has snapped, and the pressure hull is groaning heavily.")
    print("Outside, a massive bioluminescent structure shifts under centuries of silt.")

    while True:
        if metrics["integrity"] <= 0:
            print_header("CRITICAL FAILURE - AEGIR STATION CRUSHED")
            print("The structural integrity has hit 0%. The abyssal pressure ruptures the main viewport.")
            print("The icy black depths of the Pacific flood Aegir Station in a microsecond.")
            print("GAME OVER.")
            break
        if metrics["psychosis"] >= 100:
            print_header("CRITICAL FAILURE - TOTAL PSYCHOSIS")
            print("Crew psychosis has reached 100%. Chief Medical Officer Dr. Vance overrides the airlock.")
            print("The remaining crew step into the black water willingly, welcoming the Drowned Royalty.")
            print("GAME OVER.")
            break
        if metrics["wake"] >= 100:
            print_header("CRITICAL FAILURE - THE LEVIATHAN AWAKES")
            print("Leviathan Wake has reached 100%. The oceanic tectonic plates violently shatter.")
            print("The ancient entity breaches the trench, consuming Aegir Station as Lemuria rises.")
            print("GAME OVER.")
            break

        print(
            f"\n[STATUS] Integrity: {metrics['integrity']}% | "
            f"Psychosis: {metrics['psychosis']}% | "
            f"Leviathan Wake: {metrics['wake']}%"
        )

        if random.random() < 0.25:
            print("\n[ALERT: ENVIRONMENTAL ANOMALY DETECTED]")
            anomalies = [
                (
                    "A burst of bioluminescent radiation flashes through the viewport. The crew begins screaming.",
                    "psychosis",
                    15,
                ),
                (
                    "A sudden seismic tremor rocks the trench floor. The structural frame buckles.",
                    "integrity",
                    -10,
                ),
                (
                    "A low-frequency sonic hum vibrates through the metal flooring. The water temperature spikes.",
                    "wake",
                    15,
                ),
            ]
            desc, stat, val = random.choice(anomalies)
            print(f">> {desc}")
            metrics[stat] += val
            continue

        if phase == 1:
            print("\n--- PHASE 1: THE BREACH ---")
            print(
                "[AUDIO LOG] Dr. Aris (Archaeologist): "
                "'The inscriptions on the bedrock... they aren't geological features. "
                "It's a door. And something is trying to push back up.'"
            )
            print("\nCHOOSE YOUR NEXT STRATEGIC COMMAND:")
            print("1) Open the external airlock to manually clear the drill bit.")
            print("2) Flood the main shaft with heavy stabilizing fluid.")
            print("3) Initiate emergency structural lockdown and review telemetry.")
            print("4) Terminate project and abort simulation.")

            choice = input("\nEnter command (1-4): ").strip()
            if choice == "1":
                metrics["integrity"] -= 15
                metrics["psychosis"] += 20
                print(
                    "\n[LOG] Airlock opened. The structural pressure frame buckles. "
                    "Crew reports hearing telepathic whispering."
                )
                phase = 2
            elif choice == "2":
                metrics["wake"] += 25
                print(
                    "\n[LOG] Stabilizing fluid deployed. The deep-sea pulsing accelerates. "
                    "The chemical compounds are acting as a catalyst."
                )
                phase = 2
            elif choice == "3":
                metrics["psychosis"] += 5
                print(
                    "\n[LOG] Blast doors sealed. Telemetry arrays pick up distinct, "
                    "humanoid thermal signatures ascending from the trench."
                )
                phase = 2
            elif choice == "4":
                print("\nDisconnecting Celestial Portal... Goodbye.")
                break
            else:
                print("\n[ERROR] Command unrecognized. Input corrupted.")

        elif phase == 2:
            print("\n--- PHASE 2: THE INVERSION ---")
            print(
                "[AUDIO LOG] Commander Hayes: "
                "'The water... it's changing color inside the pipes. It looks like oil, "
                "but it's glowing. Dr. Vance has locked herself in the lab.'"
            )
            print("\nCHOOSE YOUR NEXT STRATEGIC COMMAND:")
            print("1) Order a complete manual blackout to hide the station's light signature.")
            print(
                "2) Overload the primary fusion reactor to pulse a massive electrical "
                "discharge through the surrounding water."
            )
            print("3) Send a diving team out into the silt to plant structural anchor charges.")
            print("4) Terminate project and abort simulation.")

            choice = input("\nEnter command (1-4): ").strip()
            if choice == "1":
                metrics["psychosis"] += 25
                print(
                    "\n[LOG] Station plunged into total pitch-blackness. In the dark, "
                    "the crew begins suffering violent hallucinations of drowned royalty."
                )
                phase = 3
            elif choice == "2":
                metrics["integrity"] -= 20
                metrics["wake"] += 20
                print(
                    "\n[LOG] EMP shockwave deployed. The thermal signature below screams "
                    "on the audio feed. Electrical grid heavily damaged."
                )
                phase = 3
            elif choice == "3":
                metrics["integrity"] += 10
                metrics["psychosis"] += 15
                print(
                    "\n[LOG] Anchors deployed successfully, stabilizing the station frame. "
                    "However, the diving team's comms went completely silent."
                )
                phase = 3
            elif choice == "4":
                print("\nDisconnecting Celestial Portal... Goodbye.")
                break
            else:
                print("\n[ERROR] Command unrecognized. Input corrupted.")

        elif phase == 3:
            print("\n--- PHASE 3: THE ABYSSAL DESCENT ---")
            print(
                "[AUDIO LOG] Dr. Vance (Static-heavy): "
                "'The Great Leviathan doesn't want to destroy us... it wants to be breathed in. "
                "The pressure is beautiful.'"
            )
            print("\nCHOOSE YOUR FINAL STRATEGIC COMMAND:")
            print("1) Initiate emergency evacuation via the hyperbaric escape pods.")
            print("2) Detonate the central reactor to vaporize Aegir Station and seal the rift forever.")
            print("3) Surrender the station controls entirely to the telepathic frequencies.")
            print("4) Terminate project and abort simulation.")

            choice = input("\nEnter command (1-4): ").strip()
            if choice == "1":
                if metrics["integrity"] > 50:
                    print_header("SURVIVAL ENDING - DECOMPRESSION ESCAPE")
                    print(
                        "Two pods make it to the surface. The survivors are heavily traumatized, "
                        "but the truth remains buried."
                    )
                else:
                    print_header("TRAGIC ENDING - ESCAPE POD COLLAPSE")
                    print(
                        "The weak hull structure collapses during launch. "
                        "The escape pods implode instantly in the trench."
                    )
                break
            elif choice == "2":
                print_header("SACRIFICE ENDING - THE EMPEROR'S REVENGE")
                print(
                    "A thermonuclear blinding flash vaporizes Aegir Station. "
                    "Lemuria remains sealed beneath millions of tons of oceanic rock."
                )
                break
            elif choice == "3":
                print_header("BAD ENDING - ASCENSION OF LEMURIA")
                print(
                    "You open all internal hatches. The crew welcomes the abyssal sea into their lungs. "
                    "They adapt. They change. They ascend."
                )
                break
            elif choice == "4":
                print("\nDisconnecting Celestial Portal... Goodbye.")
                break
            else:
                print("\n[ERROR] Command unrecognized. Input corrupted.")


if __name__ == "__main__":
    try:
        start_game()
    except (KeyboardInterrupt, EOFError):
        print("\n[SYSTEM] Link severed. Celestial Portal offline. NON SOLUS.")
        sys.exit(0)
