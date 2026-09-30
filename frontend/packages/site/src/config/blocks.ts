import type { ConfigType } from '@plone/registry';
// @ts-expect-error Webpack resolve isso via alias do Volto, mas o TS não consegue sem mapeamento explícito
import { createThemeDefinition } from '@simplesconsultoria/volto-light-theme/config/blocks';

export default function installBlocks(config: ConfigType) {
  // Define os 4 temas utilizando o sistema padrão do sc-vlt
  const customThemes = [
    createThemeDefinition('default', 'Default'),
    createThemeDefinition('darkBlue', 'DarkBlue'),
    createThemeDefinition('lightBlue', 'LightBlue'),
    createThemeDefinition('whiteB', 'WhiteB'),
  ];

  if (config.blocks) {
    config.blocks.themes = customThemes;

    // Atualiza o gridBlock para receber os temas também
    const gridBlock = config.blocks.blocksConfig?.gridBlock as any;
    if (gridBlock) {
      gridBlock.themes = customThemes;

      if (gridBlock.blocksConfig?.gridBlock) {
        gridBlock.blocksConfig.themes = customThemes;
      }
    }
  }

  return config;
}
