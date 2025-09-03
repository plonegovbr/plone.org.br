import type { ConfigType } from '@plone/registry';
import Libras from '@plonegovbr/volto-vlibras/components/Libras';

export default function install(config: ConfigType) {
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['pt-br'];
  config.settings.defaultLanguage = 'pt-br';

  // Navigation
  config.settings.navDepth = 3;

  // Display Plone Login Form
  config.settings.showPloneLogin = true;

  // Image Crop widget
  config.settings.image_crop_aspect_ratios = [
    {
      label: '16:9',
      ratio: 16 / 9,
    },
    {
      label: '4:3',
      ratio: 4 / 3,
    },
    {
      label: '1:1',
      ratio: 1,
    },
  ];

  // VLibras
  config.settings.appExtras = [
    ...config.settings.appExtras,
    {
      match: '',
      component: Libras,
    },
  ];

  return config;
}
