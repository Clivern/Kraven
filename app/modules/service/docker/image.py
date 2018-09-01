"""
Image Module
"""

# standard library
from io import BytesIO

# local Django
from .auth import Auth


class Image(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def pull(self, repository, tag=None):
        return self._client.images.pull(repository, tag)

    def build(self, fileobj, tag, rm=False, nocache=False):
        return self._client.images.build(
            fileobj=BytesIO(fileobj.encode('ascii')),
            tag=tag,
            rm=rm,
            nocache=nocache
        )

    def prune(self, filters=None):
        return self._client.images.prune(filters)

    def prune_unused(self):
        return self._client.images.prune({"dangling": True})

    def prune_all_unused(self):
        return self._client.images.prune({"dangling": False})

    def remove_by_name(self, repository, tag, force=False, noprune=False):
        return self._client.images.remove(
            image="%s:%s" % (repository, tag),
            force=force,
            noprune=noprune
        )

    def remove_by_id(self, long_id, force=False, noprune=False):
        return self._client.images.remove(
            image=long_id,
            force=force,
            noprune=noprune
        )

    def list(self, **kwargs):
        result = []
        images_list = self._client.images.list(**kwargs)
        for image in images_list:
            result.append({
                "long_id": image.id,
                "short_id": image.short_id,
                "labels": image.labels,
                "tags": image.tags,
            })
        return result

    def get_by_id(self, long_id):
        return self._client.images.get(long_id)

    def tag_by_id(self, long_id, repository, tag=None, force=False):
        image = self._client.images.get(long_id)
        if image is not False:
            return image.tag(repository, tag, force=force)
        return False

    def search(self, term):
        search_result = self._client.images.search(term=term)
        result = []
        for item in search_result:
            result.append({
                "name": item["name"],
                "star_count": item["star_count"],
                "is_automated": item["is_automated"],
                "is_official": item["is_official"],
                "description": item["description"]
            })
        return result
