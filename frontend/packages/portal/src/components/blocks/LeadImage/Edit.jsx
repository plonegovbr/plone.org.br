import React from 'react';
import PropTypes from 'prop-types';
import { defineMessages, useIntl } from 'react-intl';
import cx from 'classnames';
import { Message } from 'semantic-ui-react';
import LeadImageSidebar from '@plonegovbr/portal/components/blocks/LeadImage/LeadImageSidebar';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import config from '@plone/volto/registry';
import imageBlockSVG from '@plone/volto/components/manage/Blocks/Image/block-image.svg';
import {
  getImageField,
  hasImageField,
} from '@plonegovbr/portal/components/blocks/LeadImage/utils';

const messages = defineMessages({
  ImageBlockInputPlaceholder: {
    id: "Upload a lead image in the 'Lead Image' content field.",
    defaultMessage: "Upload a lead image in the 'Lead Image' content field.",
  },
});

const Edit = (props) => {
  const intl = useIntl();
  const { data, properties, selected } = props;

  const placeholder = () =>
    data.placeholder || intl.formatMessage(messages.ImageBlockInputPlaceholder);

  const Image = config.getComponent({ name: 'Image' }).component;
  const hasImage = hasImageField(properties);
  const [fieldName, imageField] = getImageField(properties);
  const hasImageData = imageField?.data;
  const className = cx('responsive', { 'full-image': data.align === 'full' });
  const altText = data.image_caption || properties.image_caption || '';

  return (
    <div
      className={cx(
        'block image align',
        {
          center: !Boolean(data.align),
        },
        data.align,
      )}
    >
      {!hasImage && (
        <Message>
          <center>
            <img src={imageBlockSVG} alt="" />
            <div className="message-text">{placeholder}</div>
          </center>
        </Message>
      )}
      {hasImage && hasImageData && (
        <img
          className={className}
          src={`data:${imageField['content-type']};base64,${imageField.data}`}
          width={imageField.width}
          height={imageField.height}
          alt={altText}
          style={{
            aspectRatio: `${imageField.width}/${imageField.height}`,
          }}
        />
      )}
      {hasImage && !hasImageData && (
        <Image
          className={className}
          item={properties}
          imageField={fieldName}
          sizes={(() => {
            return data.align === 'full' || data.align === 'center'
              ? '100vw'
              : data.align === 'left' || data.align === 'right'
                ? '50vw'
                : undefined;
          })()}
          alt={altText}
        />
      )}
      <SidebarPortal selected={selected}>
        <LeadImageSidebar {...props} />
      </SidebarPortal>
    </div>
  );
};

export default Edit;
Edit.propTypes = {
  properties: PropTypes.objectOf(PropTypes.any).isRequired,
  selected: PropTypes.bool.isRequired,
  block: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  pathname: PropTypes.string.isRequired,
  onChangeBlock: PropTypes.func.isRequired,
  openObjectBrowser: PropTypes.func.isRequired,
};
