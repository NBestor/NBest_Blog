import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

function UserList({ emptyText, items, onToggleFollow, showAction = false, title }) {
  return (
    <section className="content-panel relation-panel">
      <h2>{title}</h2>
      {items.length === 0 ? (
        <p className="empty-text">{emptyText}</p>
      ) : (
        <div className="relation-list">
          {items.map((item) => {
            const displayName = item.nickname || item.username;
            const showLoginName = item.username && item.nickname && item.username !== item.nickname;

            return (
              <article className="relation-item" key={item.id}>
                <div className="relation-avatar">{displayName[0]}</div>
                <div>
                  <h3>{displayName}</h3>
                  {showLoginName ? <p>@{item.username}</p> : null}
                  <div className="relation-tags">
                    {item.is_following && <span>已关注</span>}
                    {item.is_friend && <span>好友</span>}
                    <span>{item.role === 'admin' ? '管理员' : '用户'}</span>
                  </div>
                </div>
                {showAction && (
                  <button
                    className={item.is_following ? 'secondary-button' : 'follow-button'}
                    type="button"
                    onClick={() => onToggleFollow(item)}
                  >
                    {item.is_following ? '取消关注' : '关注'}
                  </button>
                )}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}

function FollowPage() {
  const [users, setUsers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function getRelations() {
    const [usersResponse, followingResponse, followersResponse, friendsResponse] = await Promise.all([
      httpClient.get('/users'),
      httpClient.get('/follows/following'),
      httpClient.get('/follows/followers'),
      httpClient.get('/follows/friends'),
    ]);

    return {
      users: usersResponse.data.items,
      following: followingResponse.data.items,
      followers: followersResponse.data.items,
      friends: friendsResponse.data.items,
    };
  }

  function setRelations(relations) {
    setUsers(relations.users);
    setFollowing(relations.following);
    setFollowers(relations.followers);
    setFriends(relations.friends);
  }

  useEffect(() => {
    let isMounted = true;

    async function loadRelations() {
      try {
        const relations = await getRelations();
        if (isMounted) {
          setRelations(relations);
        }
      } catch {
        if (isMounted) {
          setErrorMessage('关注关系加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadRelations();

    return () => {
      isMounted = false;
    };
  }, []);

  async function refreshRelations() {
    setErrorMessage('');
    setIsLoading(true);

    try {
      setRelations(await getRelations());
    } catch {
      setErrorMessage('关注关系加载失败');
    } finally {
      setIsLoading(false);
    }
  }

  async function handleToggleFollow(user) {
    try {
      if (user.is_following) {
        await httpClient.delete(`/follows/${user.id}`);
      } else {
        await httpClient.post(`/follows/${user.id}`);
      }

      await refreshRelations();
    } catch {
      setErrorMessage('操作失败，请稍后重试');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>关注关系</h1>
        <p>管理关注、粉丝与互相关注的好友。</p>
      </div>

      {isLoading ? <div className="content-panel">正在加载关注关系...</div> : null}
      {errorMessage ? <p className="form-error relation-error">{errorMessage}</p> : null}

      {!isLoading && (
        <div className="relation-grid">
          <UserList
            emptyText="暂无其他用户"
            items={users}
            onToggleFollow={handleToggleFollow}
            showAction
            title="用户列表"
          />
          <UserList emptyText="还没有关注任何人" items={following} title="我的关注" />
          <UserList emptyText="还没有粉丝" items={followers} title="我的粉丝" />
          <UserList emptyText="还没有互相关注的好友" items={friends} title="我的好友" />
        </div>
      )}
    </section>
  );
}

export default FollowPage;
