import os

# export GOOGLE_APPLICATION_CREDENTIALS=bag-finder-test1-f6157c02644e.json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'bag-finder-test1.json'


# google api 사용
def localize_objects(path, objname):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    boundary_list = []
    print('.. processing {}'.format(path))
    for object_ in objects:
        if object_.name == objname:
            boundary_list = object_.bounding_poly.normalized_vertices
            # boundary_list.append(object_.bounding_poly.normalized_vertices[0])
            # boundary_list.append(object_.bounding_poly.normalized_vertices[2])
            break

    return boundary_list










