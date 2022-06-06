import { defineMessages } from 'react-intl';
import { pull } from 'lodash';

const messages = defineMessages({
  color: {
    id: 'Color',
    defaultMessage: 'Color',
  },
  buttonText: {
    id: 'Button text',
    defaultMessage: 'Button text',
  },
  slideBackgroundColor: {
    id: 'Slide Background Color',
    defaultMessage: 'Slide Background Color',
  },
  flagColor: {
    id: 'Flag color',
    defaultMessage: 'Flag color',
  },
  flagAlign: {
    id: 'Flag align',
    defaultMessage: 'Flag align',
  },
});

const SLIDER_COLORS = [
  { name: 'blue', label: 'Blue' },
  { name: 'green', label: 'Green' },
];

export const sliderBlockSchemaEnhancer = ({ formData, schema, intl }) => {
  schema.properties.slides.schema.fieldsets[0].fields.push('buttonText');
  schema.properties.slides.schema.properties.buttonText = {
    title: intl.formatMessage(messages.buttonText),
  };
  schema.properties.slides.schema.fieldsets[0].fields.push('flagAlign');
  schema.properties.slides.schema.properties.flagAlign = {
    widget: 'inner_align',
    title: intl.formatMessage(messages.flagAlign),
    actions: ['left', 'right'],
    default: 'left',
  };
  schema.properties.slides.schema.fieldsets[0].fields.push('flagColor');
  schema.properties.slides.schema.properties.flagColor = {
    widget: 'color_picker',
    title: intl.formatMessage(messages.flagColor),
    colors: SLIDER_COLORS,
    default: 'blue',
  };
  return schema;
};

export const SliderStylingSchema = ({ schema, formData, intl }) => {
  schema.fieldsets[0].fields.push('backgroundColor');
  // This block won't have a width handler
  pull(schema.fieldsets[0].fields, 'align');
  // schema.properties.align.actions = ['center', 'wide', 'full'];
  return schema;
};
