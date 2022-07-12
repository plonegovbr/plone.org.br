import React from 'react';
import PropTypes from 'prop-types';

import { flattenToAppURL } from '@plone/volto/helpers';

import DefaultImageSVG from '@plone/volto/components/manage/Blocks/Listing/default-image.svg';

function imageUrl(item, size) {
  let src = DefaultImageSVG;
  const field = item.image_field;
  if (field) {
    if (item.image_scales) {
      const scale = item.image_scales[field][0].scales[size];
      src = flattenToAppURL(`${item['@id']}/${scale.download}`);
    } else {
      src = flattenToAppURL(`${item['@id']}/@@images/${field}/${size}`);
    }
  }
  return src;
}

/**
 * Renders a preview image for a catalog brain result item.
 *
 */
function PreviewImage(props) {
  const { item, size = 'preview', alt, ...rest } = props;
  const src = imageUrl(item, size);

  return <img src={src} alt={alt ?? item.title} {...rest} />;
}

PreviewImage.propTypes = {
  size: PropTypes.string,
  item: PropTypes.shape({
    '@id': PropTypes.string.isRequired,
    image_field: PropTypes.string,
    title: PropTypes.string.isRequired,
  }),
};

export default PreviewImage;
