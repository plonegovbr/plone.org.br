/**
 * Add your config changes here.
 * @module config
 * @example
 * export default function applyConfig(config) {
 *   config.settings = {
 *     ...config.settings,
 *     port: 4300,
 *     listBlockTypes: {
 *       ...config.settings.listBlockTypes,
 *       'my-list-item',
 *    }
 * }
 */
import DefaultTeaserBody from '@kitconcept/volto-blocks-grid/components/Teaser/DefaultBody';

// All your imports required for the config here BEFORE this line
import '@plone/volto/config';

export default function applyConfig(config) {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['pt-br'],
    defaultLanguage: 'pt-br',
    matomoSiteId: '7',
    matomoUrlBase: 'https://stats.plone.org/',
    socialNetworks: [
      {
        id: 'twitter',
        url: 'https://twitter.com/ploneorgbr',
      },
      {
        id: 'facebook',
        url: 'https://www.facebook.com/PloneConference',
      },
      {
        id: 'youtube',
        url: 'http://youtube.com/c/PloneCMS',
      },
    ],
  };

  config.blocks.blocksConfig.teaser.variations = [
    {
      id: 'default',
      isDefault: true,
      title: 'Default',
      template: DefaultTeaserBody,
    },
  ];

  config.blocks.blocksConfig.textWithBackgroundColor.availableColors = [
    '#ebebeb',
    '#0083be',
  ];

  config.blocks = {
    ...config.blocks,
    blocksConfig: { ...config.blocks.blocksConfig },
    requiredBlocks: [],
  };
  return config;
}
