
import type {renderLayout} from 'lib/layoutUtils';
import type {DispatcherType} from '../actions';

import {BaseView} from 'lib/viewUtils';

export class RenderedLayoutView extends BaseView {

    constructor(el: HTMLElement, state: WidgetType, dispatcher: DispatcherType, layoutRenderer: renderLayout) {
        super(el, state, dispatcher);

    }

    _template(_widget: WidgetType): string {
        return 'rendered layout view';
    }
}
