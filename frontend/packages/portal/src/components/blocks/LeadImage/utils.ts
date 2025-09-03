export function hasImageField(properties) {
  return (
    properties.hasOwnProperty('image') ||
    properties.hasOwnProperty('preview_image') ||
    properties.hasOwnProperty('preview_image_link')
  );
}

export function getImageField(properties) {
  const fieldName = properties?.preview_image ? 'preview_image' : 'image';
  const imageField =
    properties?.image ||
    properties?.preview_image ||
    properties?.preview_image_link?.image;
  return [fieldName, imageField];
}
