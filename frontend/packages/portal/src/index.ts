import type { ConfigType } from '@plone/registry';
import installBlocks from '@plonegovbr/portal/config/blocks';
import installSettings from '@plonegovbr/portal/config/settings';

function applyConfig(config: ConfigType) {
  installBlocks(config);
  installSettings(config);

  return config;
}

export default applyConfig;
