import React from 'react';
import PropTypes from 'prop-types';
import { Container, List } from 'semantic-ui-react';
import SocialNetwork from './SocialNetwork';

const SocialNetworks = (props) => {
  const { networks } = props;
  return (
    <Container className={'social-networks'}>
      <List horizontal>
        {networks.map(function (network, i) {
          return (
            <List.Item key={network.id}>
              <SocialNetwork id={network.id} href={network.href} />
            </List.Item>
          );
        })}
      </List>
    </Container>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
SocialNetworks.propTypes = {
  networks: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      href: PropTypes.string.isRequired,
    }),
  ).isRequired,
};

/**
 * Default properties.
 * @property {Object} defaultProps Default properties.
 * @static
 */
SocialNetworks.defaultProps = {};

export default SocialNetworks;
