/**
 * CaseStudyView view component.
 * @module components/View/CaseStudyView
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Grid, Header, List, Segment } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';

const messages = defineMessages({
  industry: {
    id: 'case_study_industry',
    defaultMessage: 'Industry',
  },
  screenshot: {
    id: 'case_study_screenshot',
    defaultMessage: 'Screenshot',
  },
  what: {
    id: 'case_study_what',
    defaultMessage: 'What',
  },
  website: {
    id: 'website',
    defaultMessage: 'Website',
  },
  visitWebsite: {
    id: 'visit_external_website',
    defaultMessage: 'Visit external website',
  },
});

const PreviewImage = ({ content }) => {
  const { preview_image, preview_caption } = content;
  const scale_name = 'preview';
  const scale = preview_image.scales[scale_name];
  const { download, height, width } = scale;
  return (
    <img src={download} alt={preview_caption} height={height} width={width} />
  );
};

const CaseStudyDetails = ({ content, display_as = 'aside' }) => {
  const intl = useIntl();
  return (
    <Segment
      as={display_as}
      {...(display_as === 'aside' ? { floated: 'right' } : {})}
    >
      {content.preview_image && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.screenshot)}
          </Header>
          <div className={'website-image'}>
            <PreviewImage content={content} />
          </div>
        </>
      )}
      <Header dividing sub>
        {intl.formatMessage(messages.industry)}
      </Header>
      <p>{content.industry.title}</p>
      {content.remoteUrl && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.website)}
          </Header>
          <p>
            <a
              href={content.remoteUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              {intl.formatMessage(messages.visitWebsite)}
            </a>
          </p>
        </>
      )}
      {content.subjects.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.what)}
          </Header>
          <List items={content.subjects} />
        </>
      )}
    </Segment>
  );
};

/**
 * CaseStudyView view component class.
 * @function CaseStudyView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const CaseStudyView = (props) => {
  const { content } = props;

  return (
    <div
      id="page-document"
      className="ui container viewwrapper case-study-view"
    >
      <Grid>
        <Grid.Column width={7} className="mobile hidden">
          <RenderBlocks {...props} />
        </Grid.Column>
        <Grid.Column width={5} className="mobile hidden">
          <CaseStudyDetails content={content} />
        </Grid.Column>
        <Grid.Column width={12} only="mobile">
          <>
            <RenderBlocks
              {...props}
              content={{
                ...content,
                blocks_layout: {
                  items: props.content.blocks_layout.items.slice(0, 1),
                },
              }}
            />
            <CaseStudyDetails content={content} display_as="div" />
            <RenderBlocks
              {...props}
              content={{
                ...content,
                blocks_layout: {
                  items: props.content.blocks_layout.items.slice(1),
                },
              }}
            />
          </>
        </Grid.Column>
      </Grid>
    </div>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
CaseStudyView.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    preview_image: PropTypes.object,
    industry: PropTypes.shape({
      token: PropTypes.string,
      title: PropTypes.string,
    }).isRequired,
    remoteUrl: PropTypes.string.isRequired,
  }).isRequired,
};

export default CaseStudyView;
