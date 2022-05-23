export const createSlateBlock = () => {
  cy.get('.ui.basic.icon.button.block-add-button').first().click();
  cy.get('.blocks-chooser .title').contains('Text').click();
  cy.get('.ui.basic.icon.button.slate').contains('Text').click();
  return getSelectedSlateEditor();
};

export const getSelectedSlateEditor = () => {
  return cy.get('.slate-editor.selected [contenteditable=true]').click();
};

export const getSlateEditorAndType = (selector, type) => {
  return cy
    .wait(1000)
    .get(selector)
    .focus()
    .click()
    .wait(2000)
    .type(type)
    .wait(1000);
};

export const getSlateEditorAndClear = (selector) => {
  return cy.get(selector).focus().click().wait(1000).clear();
};
