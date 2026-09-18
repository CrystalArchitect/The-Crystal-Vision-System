// SPDX-License-Identifier: MIT

import React, { useEffect, useState } from 'react';
import { useUserStore } from '../../lib/userStore';
import { getCurrentUser } from '../../lib/auth';
import { getTheme, setTheme } from '../../lib/storage';

export default function SettingsPage() {
  const { currentUser, setCurrentUser } = useUserStore();
  const [theme, setThemeState] = useState<'light' | 'dark' | 'auto'>('auto');

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

    const savedTheme = getTheme();
    setThemeState(savedTheme);
  }, [currentUser, setCurrentUser]);

  const handleThemeChange = (newTheme: 'light' | 'dark' | 'auto') => {
    setThemeState(newTheme);
    setTheme(newTheme);
  };

  if (!currentUser) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>

      <div className="bg-ink-800 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Preferences</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-3">Theme</label>
            <div className="flex gap-3">
              {(['light', 'dark', 'auto'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => handleThemeChange(t)}
                  className={`px-4 py-2 rounded capitalize font-medium transition-colors ${
                    theme === t
                      ? 'bg-accent text-white'
                      : 'bg-ink-700 text-gray-300 hover:bg-ink-600'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-ink-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Danger Zone</h2>
        <p className="text-gray-400 mb-4">
          Account deletion and data export features coming in Phase 7c
        </p>
      </div>
    </div>
  );
}
