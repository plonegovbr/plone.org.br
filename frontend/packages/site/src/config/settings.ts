import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Language settings
  config.settings.defaultLanguage = 'pt-br';
  config.settings.supportedLanguages = ['pt-br'];

  return config;
}
