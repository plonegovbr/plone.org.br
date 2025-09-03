import React from 'react';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import cx from 'classnames';
import config from '@plone/volto/registry';
import { getImageField } from '@plonegovbr/portal/components/blocks/LeadImage/utils';

const View = ({ data, properties }) => {
  const Image = config.getComponent({ name: 'Image' }).component;
  const [fieldName, imageField] = getImageField(properties);
  return (
    <p
      className={cx(
        'block image align',
        {
          center: !Boolean(data.align),
        },
        data.align,
      )}
    >
      {imageField && (
        <>
          {(() => {
            const image = (
              <Image
                className={cx({ 'full-width': data.align === 'full' })}
                item={properties}
                imageField={fieldName}
                sizes={config.blocks.blocksConfig.leadimage.getSizes(data)}
                alt={properties.image_caption || ''}
                responsive={true}
              />
            );
            if (data.href) {
              return (
                <UniversalLink
                  href={data.href}
                  openLinkInNewTab={data.openLinkInNewTab}
                >
                  {image}
                </UniversalLink>
              );
            } else {
              return image;
            }
          })()}
        </>
      )}
    </p>
  );
};

export default View;
