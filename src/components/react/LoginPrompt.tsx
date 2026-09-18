// SPDX-License-Identifier: MIT

import React, { useState } from 'react';
import { X } from 'lucide-react';

interface LoginPromptProps {
  message?: string;
  onClose?: () => void;
  feature?: string;
}

export default function LoginPrompt({ message, onClose, feature }: LoginPromptProps) {
  const [isOpen, setIsOpen] = useState(true);

  const handleClose = () => {
    setIsOpen(false);
    onClose?.();
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-ink-900 rounded-lg shadow-lg max-w-sm w-full p-6">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-xl font-bold">Sign in to continue</h2>
          <button
            onClick={handleClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X size={20} />
          </button>
        </div>
        <p className="text-gray-700 dark:text-gray-300 mb-6">
          {message || `${feature ? `To ${feature},` : 'To use this feature,'} you need to be signed in.`}
        </p>
        <div className="flex gap-3">
          <a
            href="/auth/login"
            className="flex-1 bg-accent text-white py-2 px-4 rounded font-medium hover:opacity-90 text-center"
          >
            Log in
          </a>
          <a
            href="/auth/signup"
            className="flex-1 bg-gray-200 dark:bg-ink-700 text-gray-900 dark:text-gray-100 py-2 px-4 rounded font-medium hover:bg-gray-300 dark:hover:bg-ink-600 text-center"
          >
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}
