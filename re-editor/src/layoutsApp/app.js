// @flow

import Store from 'lib/Store';
import AppView from './view';
import {makeController} from './controller';
import {makeErrHandler} from './errorHandler';
import {initialState} from './state';
import ViewFactory from './views/viewFactory';

export default function app(el: HTMLElement) {
    const state = initialState();
    const store = new Store(state);
    const viewFactory = new ViewFactory(store.dispatch);
    const view = new AppView(el, initialState, store.dispatch, viewFactory);
    const ctrlr = makeController();
    const update = view.update;
    const errHandler = makeErrHandler();

    store.setController(ctrlr);
    store.setUpdater(update);
    store.setErrHandler(errHandler);
}
