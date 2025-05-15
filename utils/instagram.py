import requests
import instaloader
import re
from urllib.parse import urlparse

async def download_instagram_post(url):
    try:
        L = instaloader.Instaloader()
        
        # Extract shortcode from URL
        parsed = urlparse(url)
        path = parsed.path.split('/')
        shortcode = path[2] if len(path) > 2 else None
        
        if not shortcode:
            return None
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        media_list = []
        
        # Handle single photo/video post
        if not post.is_video and not post.typename == 'GraphSidecar':
            media_list.append({
                'type': 'photo',
                'url': post.url
            })
        elif post.is_video:
            media_list.append({
                'type': 'video',
                'url': post.video_url
            })
        else:
            # Handle carousel (multiple media)
            for node in post.get_sidecar_nodes():
                if node.is_video:
                    media_list.append({
                        'type': 'video',
                        'url': node.video_url
                    })
                else:
                    media_list.append({
                        'type': 'photo',
                        'url': node.display_url
                    })
        
        return media_list
    
    except Exception as e:
        print(f"Error downloading post: {e}")
        return None

async def download_instagram_story(url):
    try:
        # This is a simplified version - in reality, downloading stories is more complex
        # and may require authentication and special permissions
        
        # For demo purposes, we'll just extract the video/photo URL
        # Note: This might not work for all cases
        
        response = requests.get(url)
        if response.status_code == 200:
            # Try to find video URL
            video_match = re.search(r'"video_url":"([^"]+)"', response.text)
            if video_match:
                return {
                    'type': 'video',
                    'url': video_match.group(1).replace('\\', '')
                }
            
            # Try to find image URL
            image_match = re.search(r'"display_url":"([^"]+)"', response.text)
            if image_match:
                return {
                    'type': 'photo',
                    'url': image_match.group(1).replace('\\', '')
                }
        
        return None
    
    except Exception as e:
        print(f"Error downloading story: {e}")
        return None