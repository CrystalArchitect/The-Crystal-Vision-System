// SPDX-License-Identifier: MIT

import React, { useState, useRef, useEffect } from 'react';
import { User, Settings, LogOut } from 'lucide-react';
import { useUserStore } from '../../lib/userStore';
import { logout } from '../../lib/auth';

interface AuthMenuProps {
  userName?: string;
}

export default function AuthMenu({ userName }: AuthMenuProps) {
  const { currentUser, clearAuth } = useUserStore();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleLogout = async () => {
    const success = await logout();
    if (success) {
      clearAuth();
      window.location.href = '/';
    }
  };

  if (!currentUser) {
    return (
      <div className="flex gap-2">
        <a
          href="/auth/login"
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-accent"
        >
          Log In
        </a>
        <a
          href="/auth/signup"
          className="px-4 py-2 text-sm font-medium bg-accent text-white rounded hover:opacity-90"
        >
          Sign Up
        </a>
      </div>
    );
  }

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-ink-800 transition-colors"
      >
        <User size={20} />
        <span className="text-sm font-medium hidden sm:inline">
          {userName || currentUser.profile.displayName || currentUser.email.split('@')[0]}
        </span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-ink-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50">
          <div className="p-3 border-b border-gray-200 dark:border-gray-700">
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {currentUser.profile.displayName || currentUser.email.split('@')[0]}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">{currentUser.email}</p>
          </div>

          <a
            href="/account/profile"
            className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-ink-800"
          >
            <User size={16} />
            Profile
          </a>

          <a
            href="/account/settings"
            className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-ink-800"
          >
            <Settings size={16} />
            Settings
          </a>

          <button
            onClick={handleLogout}
            className="w-full text-left flex items-center gap-3 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-ink-800 border-t border-gray-200 dark:border-gray-700"
          >
            <LogOut size={16} />
            Log Out
          </button>
        </div>
      )}
    </div>
  );
}
