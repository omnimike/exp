export function test() {
    const obj1 = {
        attr: 'hello',
        arr: [1,2],
        base: 'belong',
        haste: {
            type: 'skill'
        }
    };

    const obj2 = {
        attr: 'world',
        arr: [2, 3, 4],
        name: 'red',
        haste: {
            type: 'attack'
        }
    };

    const expectedDiff = [
        {
            path: 'attr',
            type: 'change',
            oldValue: 'hello',
            value: 'world'
        },
        {
            path: 'arr.0',
            type: 'change',
            oldValue: 1,
            value: 2
        },
        {
            path: 'arr.1',
            type: 'change',
            oldValue: 2,
            value: 3
        },
        {
            path: 'arr.2',
            type: 'add',
            oldValue: undefined,
            value: 4
        },
        {
            path: 'name',
            type: 'add',
            oldValue: undefined,
            value: 'red'
        },
        {
            path: 'base',
            type: 'remove',
            oldValue: 'belong',
            value: undefined
        },
        {
            path: 'haste.type',
            type: 'change',
            oldValue: 'skill',
            value: 'attack'
        }
    ];
}
