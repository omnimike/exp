
import type {DispatcherType} from '../actions';
import type {AppStateType} from '../state';

import {RenderedLayoutView} from './renderedLayoutView';

export default class ViewFactory {

    constructor(dispatcher: DispatcherType) {
        this.__dispatcher = dispatcher;
    }

    renderedLayout(el: HTMLElement, state: AppStateType, dispatcher: ?DispatcherType) {
        return new RenderedLayoutView(el, state, dispatcher || this.__dispatcher);
    }
}
