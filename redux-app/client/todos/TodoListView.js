/* @flow */

import React from 'react';
import TodoView from './TodoView';

export default class TodoListView extends React.Component {
  render() {
    return (
      <div>
        {this.props.todos.map((todo) => {
          return <TodoView key={todo.id} {...todo} />;
        })}
      </div>
    );
  }
}
