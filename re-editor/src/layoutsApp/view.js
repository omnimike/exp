// @flow

import type {AppActionType, DispatcherType} from './actions';
import type {AppStateType} from './state';
import type {ViewFactory} from './views/viewFactory';
import type {RenderedLayoutView} from './views/renderedLayoutView';

import {BaseView} from 'lib/viewUtils';

export default class AppView extends BaseView<AppActionType, AppStateType> {

    __renderedLayoutView: RenderedLayoutView;

    constructor(el: HTMLElement, state: AppStateType, dispatcher: DispatcherType, viewFactory: ViewFactory) {
        super(el, state, dispatcher);
        this.__renderedLayoutView = viewFactory.renderedLayout(this._find('[data-id="rendered-layout"]'), state);
        this._subviews.push(
            this.__renderedLayoutView
        );
    }

    _template(): string {
        return `
            <div style="display: flex; flex-direction: row">
                <div data-id="rendered-layout" style=""></div>
            </div>
        `;
    }
}
