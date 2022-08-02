import React from 'react';
import PropTypes from 'prop-types';
import { UniversalLink, Icon } from '@plone/volto/components';
import facebookSVG from '../../icons/facebook.svg';
import githubSVG from '../../icons/github.svg';
import instagramSVG from '../../icons/instagram.svg';
import twitterSVG from '../../icons/twitter.svg';
import youtubeSVG from '../../icons/youtube.svg';
import './SocialNetwork.css';

const ICONS = {
  facebook: facebookSVG,
  github: githubSVG,
  instagram: instagramSVG,
  twitter: twitterSVG,
  youtube: youtubeSVG,
};

const SocialNetwork = (props) => {
  const { id, href } = props;
  const icon = ICONS[id];
  return (
    <UniversalLink href={href} openLinkInNewTab className={'social-network'}>
      <Icon name={icon} />
    </UniversalLink>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
SocialNetwork.propTypes = {
  id: PropTypes.string.isRequired,
  href: PropTypes.string.isRequired,
};

/**
 * Default properties.
 * @property {Object} defaultProps Default properties.
 * @static
 */
SocialNetwork.defaultProps = {};

export default SocialNetwork;
