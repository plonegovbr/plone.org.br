import type { ConfigType } from '@plone/registry';
import { hasImageField } from '@plonegovbr/portal/components/blocks/LeadImage/utils';
import EditLeadImageBlock from '@plonegovbr/portal/components/blocks/LeadImage/Edit';
import ViewLeadImageBlock from '@plonegovbr/portal/components/blocks/LeadImage/View';

export default function install(config: ConfigType) {
  // Extend LeadImageBlock
  config.blocks.blocksConfig.leadimage = {
    ...config.blocks.blocksConfig.leadimage,
    view: ViewLeadImageBlock,
    edit: EditLeadImageBlock,
    restricted: ({ properties }) => !hasImageField(properties),
  };
  return config;
}
