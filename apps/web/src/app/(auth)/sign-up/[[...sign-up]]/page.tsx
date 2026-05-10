'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSignUp } from '@clerk/nextjs';
import { API_BASE } from '@/lib/api';

type SignUpStep = 'email' | 'consents' | 'phone' | 'complete';

interface ConsentState {
  ai_processing: boolean;
  ai_training: boolean;
}

export default function SignUpPage() {
  const router = useRouter();
  const { isLoaded, signUp, setActive } = useSignUp();
  const [step, setStep] = useState<SignUpStep>('email');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [consents, setConsents] = useState<ConsentState>({
    ai_processing: false,
    ai_training: false,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otpSentTo, setOtpSentTo] = useState('');

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoaded || !signUp) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Set unsafe metadata before creating sign-up
      signUp.unsafeSetMetadata({
        consents_ai_processing: consents.ai_processing,
        consents_ai_training: consents.ai_training,
      });

      await signUp.create({
        emailAddress: email,
        password,
        firstName,
        lastName,
      });

      setStep('consents');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create account');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleConsentsSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!consents.ai_processing || !consents.ai_training) {
      setError('Please accept all consent terms to continue');
      return;
    }

    if (!isLoaded || !signUp) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Update metadata with consent values
      signUp.unsafeSetMetadata({
        consents_ai_processing: true,
        consents_ai_training: true,
      });

      // Move to phone step - Clerk will send verification code
      setStep('phone');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save consent');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSendOtp = async () => {
    if (!phone.match(/^\+65[89]\d{7}$/)) {
      setError('Invalid Singapore mobile number. Format: +65XXXXXXXX');
      return;
    }

    if (!isLoaded || !signUp) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Set phone number on Clerk sign-up
      await signUp.update({
        phoneNumber: phone,
      });

      // Prepare phone verification - Clerk sends the code via SMS
      await signUp.preparePhoneNumberVerification();
      setOtpSent(true);
      setOtpSentTo(phone);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send verification code');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoaded || !signUp) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Attempt phone verification via Clerk
      const attemptResult = await signUp.attemptPhoneNumberVerification({
        code: otp,
      });

      if (attemptResult.status === 'complete') {
        // Create session
        await setActive({ session: attemptResult.createdSessionId });

        // Record consent via backend API (STORAGE consent)
        const { getToken } = await import('@clerk/nextjs');
        const token = await getToken();

        await fetch(`${API_BASE}/api/auth/phone/verify`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            phone,
            consent_given: true,
            ai_consents: true,
            clerk_verified: true,
          }),
        });

        setStep('complete');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to verify code');
    } finally {
      setIsSubmitting(false);
    }
  };

  const updateConsent = (field: keyof ConsentState) => {
    setConsents((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  if (step === 'complete') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-xl w-full max-w-md p-8 text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-8 h-8 text-green-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Welcome to KeyStone</h1>
          <p className="text-gray-600 mb-6">Your account has been created and phone verified.</p>
          <button
            onClick={() => router.push('/app')}
            className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-xl w-full max-w-md p-8">
        {step === 'email' && (
          <form onSubmit={handleEmailSubmit}>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">Create your account</h1>
              <p className="text-gray-600">Enter your details to get started</p>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
                <p className="text-xs text-gray-500 mt-1">Minimum 8 characters</p>
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
              >
                {isSubmitting ? 'Creating account...' : 'Continue'}
              </button>
            </div>
          </form>
        )}

        {step === 'consents' && (
          <form onSubmit={handleConsentsSubmit}>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">Consent Requirements</h1>
              <p className="text-gray-600">
                To use KeyStone&apos;s AI features, we need your consent
              </p>
            </div>

            <div className="space-y-4">
              <div className="p-4 border border-gray-200 rounded-lg">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={consents.ai_processing}
                    onChange={() => updateConsent('ai_processing')}
                    className="mt-1 h-4 w-4 text-brand-500 rounded border-gray-300 focus:ring-brand-500"
                  />
                  <div>
                    <p className="font-medium text-gray-900">AI Processing Consent</p>
                    <p className="text-sm text-gray-600">
                      I consent to KeyStone processing my resume and job application data using AI
                      to provide personalized job recommendations and application optimization. My
                      data will be sent to Claude API (Anthropic) for analysis.
                    </p>
                  </div>
                </label>
              </div>

              <div className="p-4 border border-gray-200 rounded-lg">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={consents.ai_training}
                    onChange={() => updateConsent('ai_training')}
                    className="mt-1 h-4 w-4 text-brand-500 rounded border-gray-300 focus:ring-brand-500"
                  />
                  <div>
                    <p className="font-medium text-gray-900">AI Training Consent</p>
                    <p className="text-sm text-gray-600">
                      I consent to KeyStone using anonymized feedback from my application outcomes
                      to improve its AI models. Personal identifying information will never be
                      included.
                    </p>
                  </div>
                </label>
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting || !consents.ai_processing || !consents.ai_training}
                className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
              >
                {isSubmitting ? 'Saving...' : 'Accept and Continue'}
              </button>

              <button
                type="button"
                onClick={() => setStep('email')}
                className="w-full py-2 text-gray-600 hover:text-gray-900"
              >
                Back
              </button>
            </div>
          </form>
        )}

        {step === 'phone' && (
          <form onSubmit={handleVerifyOtp}>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">Verify Phone Number</h1>
              <p className="text-gray-600">We&apos;ll send a verification code to your phone</p>
            </div>

            {!otpSent ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Singapore Mobile Number
                  </label>
                  <input
                    type="tel"
                    required
                    placeholder="+65XXXXXXXX"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">Format: +65 followed by 8 digits</p>
                </div>

                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <button
                  type="button"
                  onClick={handleSendOtp}
                  disabled={isSubmitting}
                  className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
                >
                  {isSubmitting ? 'Sending...' : 'Send Verification Code'}
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700">
                  Code sent to {otpSentTo}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Verification Code
                  </label>
                  <input
                    type="text"
                    required
                    maxLength={6}
                    pattern="[0-9]{6}"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    placeholder="XXXXXX"
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-center text-2xl tracking-widest"
                  />
                </div>

                <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
                  <p className="font-medium">Storage Consent</p>
                  <p className="text-xs mt-1">
                    By verifying your phone, you acknowledge that KeyStone will store your resume
                    and application data to provide job recommendation services.
                  </p>
                </div>

                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={isSubmitting || otp.length !== 6}
                  className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
                >
                  {isSubmitting ? 'Verifying...' : 'Verify and Complete'}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setOtpSent(false);
                    setOtp('');
                    setError(null);
                  }}
                  className="w-full py-2 text-gray-600 hover:text-gray-900"
                >
                  Use a different number
                </button>
              </div>
            )}
          </form>
        )}
      </div>
    </div>
  );
}
