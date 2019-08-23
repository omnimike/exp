// @flow

import type {EventSelectorMapType} from 'lib/viewUtils';
import type {AppActionType} from './actions';
import type {AppStateType} from './state';

import {BaseView} from 'lib/viewUtils';

export default class AppView extends BaseView<AppActionType, AppStateType> {

    _template(state: AppStateType): string {
        return `
            value: <span data-id="counter">${state.count}</span>
            <button data-id="increment-button">increment</button>
            <button data-id="reset-button">reset</button>
        `;
    }

    _events(): EventSelectorMapType {
        return {
            'click [data-id="increment-button"]': this._dispatch.bind(this, {type: 'increment'}),
            'click [data-id="reset-button"]': this._dispatch.bind(this, {type: 'reset'})
        };
    }

    _render(state: AppStateType): void {
        this._find('[data-id="counter"]').innerHTML = state.count + '';
    }
}
