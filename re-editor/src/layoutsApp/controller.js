// @flow

import type {AppActionType} from './actions';
import type {AppStateType} from './state';

export type AppControllerType = (AppStateType, AppActionType) => AppStateType;

export function makeController(): AppControllerType {
    return (state: AppStateType, action: AppActionType) => {
        switch (action.type) {
        default:
            throw new Error('invalid action');
        }
    };
}
