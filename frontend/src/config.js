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

import { SliderStylingSchema } from './components/Blocks/Slider/schema';
import { sliderBlockSchemaEnhancer } from './components/Blocks/Slider/schema';
import SliderDefaultBody from './components/Blocks/Slider/DefaultBody';
import CaseStudyView from './components/View/CaseStudyView';
import SocialSharing from '@codesyntax/volto-social-sharing/SocialSharing';

// All your imports required for the config here BEFORE this line
import '@plone/volto/config';

const BG_COLORS = [
  { name: 'transparent', label: 'Transparent' },
  { name: 'grey', label: 'Grey' },
];

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
        href: 'https://twitter.com/ploneorgbr',
      },
      {
        id: 'mastodon',
        href: 'https://plone.social/@ploneorgbr',
      },
      {
        id: 'facebook',
        href: 'https://www.facebook.com/Plone-Brasil-101606785972720',
      },
      {
        id: 'instagram',
        href: 'https://www.instagram.com/plonebr/',
      },
      {
        id: 'youtube',
        href: 'http://youtube.com/c/PloneCMS',
      },
    ],
    appExtras: [
      ...config.settings.appExtras,
      {
        match: '',
        component: SocialSharing,
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

  config.blocks.blocksConfig.slider = {
    ...config.blocks.blocksConfig.slider,
    enableStyling: true,
    stylesSchema: SliderStylingSchema,
    colors: BG_COLORS,
    defaultBGColor: 'transparent',
    schemaEnhancer: sliderBlockSchemaEnhancer,
    variations: [
      {
        id: 'default',
        isDefault: true,
        title: 'Default',
        view: SliderDefaultBody,
      },
    ],
  };

  config.blocks = {
    ...config.blocks,
    blocksConfig: { ...config.blocks.blocksConfig },
    requiredBlocks: [],
  };

  config.views.contentTypesViews = {
    ...config.views.contentTypesViews,
    CaseStudy: CaseStudyView,
  };

  return config;
}
