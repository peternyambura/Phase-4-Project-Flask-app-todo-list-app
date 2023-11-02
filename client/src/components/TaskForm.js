import React, { useState } from 'react';
import axios from 'axios';

const TaskForm = (props) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    if (props.id) {
        axios.put(`/api/tasks/${props.id}`, {
            title: title,
            description: description
        })
        .then(response => {
            console.log("Task updated successfully:", response.data);
        })
        .catch(error => {
            console.error("Error updating task:", error);
        });
    } else {
        axios.post('/api/tasks', {
            title: title,
            description: description
        })
        .then(response => {
            console.log("Task created successfully:", response.data);
        })
        .catch(error => {
            console.error("Error creating task:", error);
        });
    }
};


  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={title} 
        onChange={e => setTitle(e.target.value)} 
        placeholder="Task Title" 
      />
      <textarea 
        value={description} 
        onChange={e => setDescription(e.target.value)} 
        placeholder="Task Description"
      />
      <button type="submit">Save</button>
    </form>
  );
}

export default TaskForm;
