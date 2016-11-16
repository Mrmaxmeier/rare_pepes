import React, { Component } from 'react';
import { PepeImage } from './Pepe.js'
import { Grid, Divider } from 'semantic-ui-react';

export class VotingLayout extends Component {
  render() {
    return (
      <Grid stackable relaxed='very'>
        <Grid.Row columns={2} style={{height: 'calc(100vh - 2.8em)', padding: 0}}>
          <Grid.Column>
            <PepeImage />
          </Grid.Column>
          <Divider vertical>vs</Divider>
          <Grid.Column>
            <PepeImage />
          </Grid.Column>
        </Grid.Row>
      </Grid>
    )
  }
}