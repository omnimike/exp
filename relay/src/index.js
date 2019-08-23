const {GraphQLServer} = require('graphql-yoga');

const typeDefs = `
type Query {
  info: String,
  owner: Person,
}

type Person {
  name: String,
}
`;

const resolvers = {
  Query: {
    info: () => 'some info about the server',
    owner: (obj, args, context, info) => {
      return {
        name: 'mike',
      };
    },
  },
};

const server = new GraphQLServer({
  typeDefs,
  resolvers,
});

server.start(() => console.log('running...'));
