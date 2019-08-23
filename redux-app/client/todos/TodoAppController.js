/* @flow */

import React from 'react';
import TodoListView from './TodoListView';

export default class TodoAppController extends React.Component {

  render() {
    return (
      <TodoListView todos={this.props.state} />
    );
  }
}
