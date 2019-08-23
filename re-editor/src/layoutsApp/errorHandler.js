// @flow

export type ErrHandlerType = (err: mixed) => void;

export function makeErrHandler(): ErrHandlerType {
    return (err: mixed) => {
        console.error(err);
    };
}
