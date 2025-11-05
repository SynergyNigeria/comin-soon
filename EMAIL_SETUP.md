# Email Setup Guide

## Problem
Render's free tier blocks outbound SMTP connections on ports 587 and 465, preventing email delivery via traditional SMTP.

## Solution: Resend API

We've implemented Resend (https://resend.com) as the primary email service with SMTP as fallback.

### Why Resend?
- ✅ **Free Tier:** 3,000 emails/month, 100 emails/day
- ✅ **HTTP API:** Works on all hosting platforms (no SMTP port restrictions)
- ✅ **Modern & Simple:** Easy to set up and use
- ✅ **Reliable:** Built for developers

## Setup Instructions

### Step 1: Create Resend Account
1. Go to https://resend.com
2. Sign up for a free account
3. Verify your email

### Step 2: Get API Key
1. Go to **API Keys** in your Resend dashboard
2. Click **Create API Key**
3. Name it "COVU Production"
4. Select "Sending access"
5. Copy the API key (starts with `re_`)

### Step 3: Add Domain (Optional but Recommended)
1. Go to **Domains** in your Resend dashboard
2. Click **Add Domain**
3. Enter your domain (e.g., `covumarket.com`)
4. Add the DNS records to your domain provider
5. Wait for verification (can take up to 48 hours)

**OR** use the default domain:
- From: `COVU <onboarding@resend.dev>`
- This works immediately but may be flagged as spam by some providers

### Step 4: Configure Environment Variables in Render

1. Go to your Render dashboard
2. Select your web service
3. Go to **Environment** tab
4. Add these variables:

```
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=COVU <noreply@covumarket.com>
```

**Note:** 
- If you haven't verified your domain, use: `COVU <onboarding@resend.dev>`
- The email backend will automatically try Resend first, then fall back to SMTP if needed

### Step 5: Deploy
Commit and push your changes. Render will automatically redeploy.

## Testing

After deployment, test the email verification:
1. Go to your website
2. Enter your email
3. Check your inbox (and spam folder)
4. You should receive the verification code within seconds

## Fallback Behavior

The system will:
1. **First:** Try Resend API (if `RESEND_API_KEY` is set)
2. **Fallback:** Try SMTP (if Resend fails or API key is missing)

This ensures maximum reliability!

## Current Status

- ✅ Resend integration complete
- ✅ Background email sending (no blocking)
- ✅ SMTP fallback implemented
- ⏳ Waiting for you to add Resend API key to Render

## Need Help?

Check Resend documentation: https://resend.com/docs/introduction
