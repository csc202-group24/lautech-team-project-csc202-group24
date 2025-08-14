# storage.py
"""
Storage analysis module.

Calculates storage usage and provides compression recommendations.
"""
class StorageAnalyzer:
    """Analyzes storage usage and suggests compression."""
    def analyze(self, images: list) -> tuple:
        """Calculate total storage and compression recommendations."""
        total_size = 0
        recommendations = []
        for img in images:
            size = img["size"]
            total_size += size
            # Heuristic: recommend compression for files > 1MB
            if size > 1024 * 1024:
                recommendations.append(
                    f"{img['path']}: Compress to reduce size ({size / (1024**2):.2f} MB)"
                )
        return total_size, recommendations
