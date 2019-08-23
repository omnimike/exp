// @flow

import Store from 'lib/Store';
import AppView from './view';
import {makeController} from './controller';
import {makeErrHandler} from './errorHandler';

export default function app(el: HTMLElement) {
    const initialState = {count: 0};
    const store = new Store(initialState);
    const view = new AppView(el, initialState, store.dispatch);
    const ctrlr = makeController();
    const update = view.update;
    const errHandler = makeErrHandler();

    store.setController(ctrlr);
    store.setUpdater(update);
    store.setErrHandler(errHandler);
}
