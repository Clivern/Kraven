"""
Image Module
"""

# local Django
from .auth import Auth


class Image(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def pull(self, repository, tag=None):
        if not self.check_health():
            return False
        return self._client.images.pull(repository, tag)

    def build(self, **kwargs):
        if not self.check_health():
            return False
        return self._client.images.build(**kwargs)

    def prune(self, filters=None):
        return self._client.images.prune(filters)

    def remove(self, image, force=False, noprune=False):
        return self._client.images.remove(
            image=image,
            force=force,
            noprune=noprune
        )

    def list(self, **kwargs):
        return self._client.images.list(**kwargs)

    def get(self, image_name):
        return self._client.images.get(image_name)

    def tag(self, image_name, repository, tag=None, force=False):
        image = self.get(image_name)
        if image is not False:
            return image.tag(repository, tag, force=force)

        return False

    def search(self, term):
        return self._client.images.search(term=term)
