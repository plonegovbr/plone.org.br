import {
  createSlateBlock,
  getSlateEditorAndType,
  getSelectedSlateEditor,
} from '../support/slate';

describe('Add Content Tests', () => {
  beforeEach(() => {
    // give a logged in editor and the site root
    cy.autologin();
    cy.visit('/');
    cy.viewport('macbook-16');
    cy.waitForResourceToLoad('@navigation');
    cy.waitForResourceToLoad('@breadcrumbs');
    cy.waitForResourceToLoad('@actions');
    cy.waitForResourceToLoad('@types');
  });
  it('As editor I can add a page', function () {
    // when I add a page
    cy.get('#toolbar-add').click();
    cy.get('#toolbar-add-document').click();
    cy.get('.documentFirstHeading')
      .type('My Page')
      .get('.documentFirstHeading')
      .contains('My Page');

    // then I a new page has been created
    cy.get('#toolbar-save').click();
    cy.url().should('eq', Cypress.config().baseUrl + '/my-page');
    if (Cypress.env('API') === 'plone') {
      cy.get('.navigation .item.active').should('have.text', 'My Page');
    } else {
      cy.contains('My Page');
    }
  });

  it('As editor I can add a page with a text block', function () {
    // when I add a page with a text block
    cy.get('#toolbar-add').click();
    cy.get('#toolbar-add-document').click();
    cy.get('.documentFirstHeading')
      .type('My Page')
      .get('.documentFirstHeading')
      .contains('My Page');

    getSlateEditorAndType(
      '.block .slate-editor [contenteditable=true]',
      'This is the text',
    );

    getSelectedSlateEditor().contains('This is the text');
    cy.get('#toolbar-save').click();
    cy.url().should('eq', Cypress.config().baseUrl + '/my-page');
  });
});
