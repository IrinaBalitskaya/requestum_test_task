import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resultList, setResultList] = useState([]);

  const handleButtonClick = async (
  ) => {
    try {
      setIsLoading(true);
      const axiosConfig = axios.create();
      const response = await axiosConfig.get(
        '/api/github_projects/get-common-contributors-repos/',
        {
          params: {
            github_repo_url: inputValue,
          },
        },
      );

      if (response.data) {
        setResultList(response.data);
        setError(null);
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.github_repo_url) {
        setError(`Validation Error: ${error.response.data.github_repo_url[0]}`);
      } else {
        console.error('Error:', error);
        setError('Error fetching data');
      }
    } finally {
      setIsLoading(false);
    }
  }; // This will fetch data when the component mounts

  return (
    <>
      <input type="text" value={inputValue} onChange={e => setInputValue(e.target.value)} />
      <button onClick={handleButtonClick} disabled={isLoading || !inputValue}>
        Submit
      </button>
      {isLoading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : <p><strong>Similar to {inputValue}</strong></p>}
      { resultList &&
        <>
            <ul>
              {resultList.map((repo, index) => (
                <li key={index}>
                  <strong>URL:</strong> <a href={repo.url}>{repo.name}</a>
                  <br />
                  <strong>Common Contributors Count:</strong> {repo.common_contributors_count}
                  <hr />
                </li>
              ))}
            </ul>
        </>
      }
    </>
  );
};

export default App;