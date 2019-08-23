// @flow

export type IncrementActionType = {
    type: 'increment'
};

export type ResetActionType = {
    type: 'reset'
};

export type AppActionType = IncrementActionType | ResetActionType;
