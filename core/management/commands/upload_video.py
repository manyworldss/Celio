import os
import logging
from django.core.management.base import BaseCommand
from vercel_blob import blob_store
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Command(BaseCommand):
    help = 'Uploads the demo video to Vercel Blob storage.'

    def handle(self, *args, **options):
        # Get the Vercel Blob token from environment variables
        vercel_blob_token = os.environ.get('VERCEL_BLOB_TOKEN')
        if not vercel_blob_token:
            self.stdout.write(self.style.ERROR('VERCEL_BLOB_TOKEN environment variable is not set.'))
            self.stdout.write('Please set the VERCEL_BLOB_TOKEN in your .env file.')
            return

        video_path = 'media/emergency_cards/Recording 2025-07-09 143911.mp4'
        
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f'Video file not found at {video_path}')

            with open(video_path, 'rb') as f:
                # Configure the blob store with the token from environment variables
                blob = blob_store.put(
                    os.path.basename(video_path),
                    f.read(),
                    options={
                        'access': 'public',
                        'token': vercel_blob_token
                    }
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully uploaded video to {blob["url"]}'))
            
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            logger.error(f'File not found: {e}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            logger.error(f'Error uploading video: {e}')