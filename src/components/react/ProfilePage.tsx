// SPDX-License-Identifier: MIT

import React, { useEffect } from 'react';
import { useUserStore } from '../../lib/userStore';
import { getCurrentUser } from '../../lib/auth';

export default function ProfilePage() {
  const { currentUser, setCurrentUser } = useUserStore();

  useEffect(() => {
    const loadUser = async () => {
      if (!currentUser) {
        const user = await getCurrentUser();
        if (user) {
          setCurrentUser(user);
        } else {
          window.location.href = '/auth/login';
        }
      }
    };
    loadUser();
  }, [currentUser, setCurrentUser]);

  if (!currentUser) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Profile</h1>

      <div className="bg-ink-800 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Account Information</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-2">Display Name</label>
            <p className="text-lg">
              {currentUser.profile.displayName || 'Not set'}
            </p>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-2">Email</label>
            <p className="text-lg">{currentUser.email}</p>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-2">Member Since</label>
            <p className="text-lg">
              {new Date(currentUser.createdAt).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-400">
        <p>Full profile editing coming in Phase 7c</p>
      </div>
    </div>
  );
}
