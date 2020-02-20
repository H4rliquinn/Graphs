import random

class User:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i+1}")

        # Create friendships
        # create a list with all possible friendships
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))


        # Shuffle the list
        random.shuffle(possible_friendships)
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

        # avg_friendships = total_friendships / num_users
        # total_friendships = avg_friendships * num_users
        # N = avg_friendships * num_users // 2


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}
        q=Queue()
        q.enqueue([user_id])
        while q.size()>0:
            curr=q.dequeue()
            if not visited.get(curr[-1],None):
                visited[curr[-1]]=curr

            for nxt in self.friendships[curr[-1]]:
                if nxt not in visited:
                    new_q=curr.copy()
                    new_q.append(nxt)
                    q.enqueue(new_q)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    connections = sg.get_all_social_paths(1)
    # print("USERS",sg.users)
    # print("------------")
    print("FRIENDSHIPS",sg.friendships)
    print("------------")
    print("CONNECTIONS",connections)
    print("------------")
    print("Friend Count: ", len(connections))
    sum_connections=0
    for x in connections:
        sum_connections+=len(connections[x])
    print(f"In {len(connections)} connections, avg degree of separation is: {round(sum_connections/len(connections),2)}")