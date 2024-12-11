import { useState, useEffect } from 'react';
import axios from 'axios';
import UserList from './userList'
import UserForm from './userForm';


function App() {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState({})
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    fetchUser()
  }, []);

  const fetchUser = async () => {
    axios.get('http://127.0.0.1:5000/api/user')
      .then(response => setUsers(response.data))
      .catch(error => console.error("Error fetching users:", error));
  }



  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentUser({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (user) => {
    if (isModalOpen) return
    setCurrentUser(user)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchUser()
  }
  return (
    <div>
      <UserList users={users} updateUser={openEditModal} updateCallback={onUpdate} />


      <h1>List of Users</h1>
      <ul>

      </ul>
      <UserForm existingUser={currentUser} updateCallback={onUpdate} />
    </div >
  );
}

export default App;
