/* @flow */

import React from 'react';

export default class TodoView extends React.Component {
  render() {
    return (
      <div>{this.props.text}</div>
    );
  }
}
