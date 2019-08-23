// @flow

import type {AppActionType} from './actions';
import type {AppStateType} from './state';

export type AppControllerType = (AppStateType, AppActionType) => AppStateType;

export function makeController(): AppControllerType {
    return (state: AppStateType, action: AppActionType) => {
        switch (action.type) {
        case 'increment':
            return Object.assign({}, state, {count: state.count + 1});
        case 'reset':
            return Object.assign({}, state, {count: 0});
        default:
            throw new Error('invalid action');
        }
    };
}
