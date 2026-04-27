import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

FROM_EMAIL = "noreply@orbitsoccer.com"
FROM_NAME = "OrbitSoccer"

def send_email(to: str, subject: str, html: str):
    try:
        resend.Emails.send({
            "from": f"{FROM_NAME} <{FROM_EMAIL}>",
            "to": to,
            "subject": subject,
            "html": html
        })
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def email_coach_new_request(coach_email: str, coach_name: str, player_name: str, player_age: int, player_position: str, focus_areas: list, amount: float):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
            <p style="color: #555; margin: 8px 0 0;">Pro Review Platform</p>
        </div>
        
        <div style="background: #111; border: 1px solid #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h2 style="color: #a855f7; margin: 0 0 16px;">📥 New Review Request!</h2>
            <p style="color: #aaa;">Hi Coach {coach_name},</p>
            <p style="color: #aaa;">You have a new video review request from a parent on OrbitSoccer!</p>
            
            <div style="background: #1a1a1a; border-radius: 10px; padding: 16px; margin: 16px 0;">
                <p style="color: #555; font-size: 12px; text-transform: uppercase; margin: 0 0 8px;">Player Details</p>
                <p style="color: white; margin: 4px 0;"><strong>Name:</strong> {player_name}</p>
                <p style="color: white; margin: 4px 0;"><strong>Age:</strong> {player_age}</p>
                <p style="color: white; margin: 4px 0;"><strong>Position:</strong> {player_position}</p>
                <p style="color: white; margin: 4px 0;"><strong>Focus Areas:</strong> {', '.join(focus_areas)}</p>
                <p style="color: #d4ff00; margin: 4px 0;"><strong>Your Earnings:</strong> ${amount * 0.75:.2f}</p>
            </div>
            
            <p style="color: #aaa;">Please log in to your coach portal to review and respond within 24 hours.</p>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com/pro-coach-portal" 
                   style="background: #a855f7; color: white; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    View Request →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(coach_email, f"New Review Request — {player_name}", html)

def email_parent_request_received(parent_email: str, player_name: str, coach_name: str, include_zoom: bool):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
            <p style="color: #555; margin: 8px 0 0;">Pro Review Platform</p>
        </div>
        
        <div style="background: #111; border: 1px solid #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h2 style="color: #00ffc8; margin: 0 0 16px;">✅ Review Request Received!</h2>
            <p style="color: #aaa;">Your review request for <strong style="color: white;">{player_name}</strong> has been submitted to <strong style="color: white;">Coach {coach_name}</strong>.</p>
            
            <div style="background: #1a1a1a; border-radius: 10px; padding: 16px; margin: 16px 0;">
                <p style="color: #aaa; margin: 4px 0;">⏱ Expected response: <strong style="color: white;">Within 24 hours</strong></p>
                {'<p style="color: #aaa; margin: 4px 0;">📅 Zoom call link will be sent with the response</p>' if include_zoom else ''}
            </div>
            
            <p style="color: #aaa;">We will email you as soon as Coach {coach_name} submits their feedback. You can also check the app for updates.</p>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com" 
                   style="background: #00ffc8; color: #0a0a0a; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    Open OrbitSoccer →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(parent_email, f"Review Request Received — {player_name}", html)

def email_parent_review_complete(parent_email: str, player_name: str, coach_name: str, zoom_link: str = None):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
            <p style="color: #555; margin: 8px 0 0;">Pro Review Platform</p>
        </div>
        
        <div style="background: #111; border: 1px solid #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h2 style="color: #d4ff00; margin: 0 0 16px;">🎉 Your Review is Ready!</h2>
            <p style="color: #aaa;">Coach <strong style="color: white;">{coach_name}</strong> has completed the video review for <strong style="color: white;">{player_name}</strong>!</p>
            
            {'<div style="background: #0a2a1a; border: 1px solid #00ffc830; border-radius: 10px; padding: 16px; margin: 16px 0;"><p style="color: #00ffc8; margin: 0;">📅 Zoom Call Link: <a href="' + zoom_link + '" style="color: #00ffc8;">' + zoom_link + '</a></p></div>' if zoom_link else ''}
            
            <p style="color: #aaa;">Log in to OrbitSoccer to read the full coaching analysis and feedback.</p>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com" 
                   style="background: #d4ff00; color: #0a0a0a; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    View Feedback →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(parent_email, f"Your Review is Ready — {player_name}", html)

def email_player_drill_assigned(player_email: str, player_name: str, drill_title: str, coach_name: str):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
        </div>
        
        <div style="background: #111; border: 1px solid #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h2 style="color: #d4ff00; margin: 0 0 16px;">🎯 New Drill Assigned!</h2>
            <p style="color: #aaa;">Hi {player_name}!</p>
            <p style="color: #aaa;">Coach <strong style="color: white;">{coach_name}</strong> has assigned you a new drill:</p>
            
            <div style="background: #1a1a1a; border-radius: 10px; padding: 16px; margin: 16px 0; text-align: center;">
                <p style="color: #d4ff00; font-size: 20px; font-weight: bold; margin: 0;">{drill_title}</p>
            </div>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com" 
                   style="background: #d4ff00; color: #0a0a0a; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    Start Training →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(player_email, f"New Drill Assigned — {drill_title}", html)

def email_streak_reminder(player_email: str, player_name: str, current_streak: int):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
        </div>
        
        <div style="background: #111; border: 1px solid #ff6b0050; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔥</div>
            <h2 style="color: #ff6b00; margin: 0 0 16px;">Don't Break Your Streak!</h2>
            <p style="color: #aaa;">Hi {player_name}!</p>
            <p style="color: #aaa;">You haven't trained in a few days. Don't let your {current_streak} day streak disappear!</p>
            
            <div style="background: #1a1a1a; border-radius: 10px; padding: 16px; margin: 16px 0;">
                <p style="color: #ff6b00; font-size: 32px; font-weight: bold; margin: 0;">🔥 {current_streak} days</p>
                <p style="color: #555; margin: 4px 0 0;">Current streak</p>
            </div>
            
            <p style="color: #aaa;">Just 10 minutes of training today will keep your streak alive!</p>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com" 
                   style="background: #ff6b00; color: white; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    Train Now →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(player_email, f"Don't break your streak, {player_name}! 🔥", html)

def email_milestone_reached(player_email: str, player_name: str, milestone: str):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
        </div>
        
        <div style="background: #111; border: 1px solid #d4ff0050; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">🏆</div>
            <h2 style="color: #d4ff00; margin: 0 0 16px;">Milestone Reached!</h2>
            <p style="color: #aaa;">Amazing work {player_name}!</p>
            
            <div style="background: #1a1a1a; border-radius: 10px; padding: 16px; margin: 16px 0;">
                <p style="color: #d4ff00; font-size: 20px; font-weight: bold; margin: 0;">{milestone}</p>
            </div>
            
            <p style="color: #aaa;">Keep training and reach even greater heights!</p>
            
            <div style="text-align: center; margin-top: 24px;">
                <a href="https://orbitsoccer.com" 
                   style="background: #d4ff00; color: #0a0a0a; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                    View Progress →
                </a>
            </div>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(player_email, f"🏆 Milestone Reached — {milestone}!", html)

def email_announcement(to: str, subject: str, message: str, name: str = ""):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0a; color: white; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 32px;">
            <h1 style="color: #00ffc8; font-size: 28px; margin: 0;">ORBIT<span style="color: white;">SOCCER</span></h1>
            <p style="color: #555; margin: 8px 0 0;">Official Announcement</p>
        </div>
        
        <div style="background: #111; border: 1px solid #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            {f'<p style="color: #aaa;">Hi {name}!</p>' if name else ''}
            <div style="color: #aaa; line-height: 1.8; white-space: pre-wrap;">{message}</div>
        </div>
        
        <div style="text-align: center; margin-top: 24px;">
            <a href="https://orbitsoccer.com" 
               style="background: #00ffc8; color: #0a0a0a; padding: 14px 32px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
                Open OrbitSoccer →
            </a>
        </div>
        
        <p style="color: #333; font-size: 12px; text-align: center; margin-top: 24px;">OrbitSoccer · orbitsoccer.com</p>
    </div>
    """
    return send_email(to, subject, html)
