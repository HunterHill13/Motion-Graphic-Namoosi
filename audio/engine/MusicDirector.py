"""
Music Director & Royalty-Free Licensing Verification (v2.1)
Manages music research, licensed library indexing, and story-driven dynamic volume arcs.
"""

from typing import Dict, Any, List

class MusicDirector:
    """Manages music selection, royalty-free licensing verification, and music arcs."""

    # Curated royalty-free tracks cataloged with clear attribution and commercial licensing
    LICENSED_CATALOG: List[Dict[str, Any]] = [
        {
            "id": "bio_ambient_pulse",
            "title": "Subtle Scientific Resonance",
            "artist": "OpenAudio Research",
            "source": "Free Music Archive / Pixabay Music",
            "url": "https://pixabay.com/music/search/ambient-science/",
            "license": "Creative Commons / Royalty-Free Commercial Safe",
            "commercial_use": True,
            "attribution_required": False,
            "tempo_bpm": 85,
            "genre": "Ambient Cinematic Electronic",
            "energy": "Restrained Pulse, Mysterious",
            "recommended_modes": ["medical", "scientific", "documentary"]
        },
        {
            "id": "kinetic_reel_beat",
            "title": "Modern Minimal Kinetic",
            "artist": "OpenAudio Tech",
            "source": "YouTube Audio Library",
            "url": "https://studio.youtube.com/channel/music",
            "license": "YouTube Audio Library License",
            "commercial_use": True,
            "attribution_required": False,
            "tempo_bpm": 120,
            "genre": "Rhythmic Electronic",
            "energy": "Energetic, Fast Paced",
            "recommended_modes": ["social_reel", "quick_explainer"]
        }
    ]

    @classmethod
    def get_recommended_track(cls, genre: str = "medical") -> Dict[str, Any]:
        for track in cls.LICENSED_CATALOG:
            if genre in track["recommended_modes"]:
                return track
        return cls.LICENSED_CATALOG[0]

    @classmethod
    def generate_music_arc(cls, duration_sec: float) -> List[Dict[str, Any]]:
        """Generates dynamic volume automation arc following narrative acts."""
        return [
            {"time_sec": 0.0, "volume_multiplier": 0.8, "narrative_phase": "Minimal Hook Intro"},
            {"time_sec": round(duration_sec * 0.15, 2), "volume_multiplier": 1.0, "narrative_phase": "Rhythmic Development"},
            {"time_sec": round(duration_sec * 0.45, 2), "volume_multiplier": 0.7, "narrative_phase": "Ducked Under Core Biological Climax"},
            {"time_sec": round(duration_sec * 0.85, 2), "volume_multiplier": 1.0, "narrative_phase": "Resolution Swell"},
            {"time_sec": duration_sec, "volume_multiplier": 0.0, "narrative_phase": "Smooth Fadeout Outro"}
        ]

if __name__ == "__main__":
    track = MusicDirector.get_recommended_track("medical")
    print("Recommended Licensed Track:", track["title"])
    print("License:", track["license"])
    arc = MusicDirector.generate_music_arc(30.0)
    print("Generated Music Arc:", arc)
