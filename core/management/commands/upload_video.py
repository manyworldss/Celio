import os
from django.core.management.base import BaseCommand
from vercel_blob import blob_store
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Uploads the demo video to Vercel Blob storage.'

    def handle(self, *args, **options):
        video_path = 'media/emergency_cards/Recording 2025-07-09 143911.mp4'
        if not os.path.exists(video_path):
            self.stdout.write(self.style.ERROR(f'Video file not found at {video_path}'))
            return

        with open(video_path, 'rb') as f:
                                    blob = blob_store.put(os.path.basename(video_path), f.read(), options={'access': 'public'})

        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded video to {blob["url"]}'))