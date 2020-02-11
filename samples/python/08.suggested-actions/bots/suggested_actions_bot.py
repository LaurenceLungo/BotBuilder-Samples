# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler, MessageFactory, CardFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    CardImage,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)

uninit = "uninit"
reserve = "reserve"
order = "order"
check = "check"

menu = [ 
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static7.orstatic.com/userphoto/photo/A/8B4/01N36I8D34B9EA6A565DABpx.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="餐蛋治",
                        display_text="餐蛋治",
                        text="餐蛋治",
                        value="餐蛋治"
                    )
                ],
            )),
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static7.orstatic.com/userphoto/photo/A/8B4/01N36I8D34B9EA6A565DABpx.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="餐蛋治",
                        display_text="餐蛋治",
                        text="餐蛋治",
                        value="餐蛋治"
                    )
                ],
            )),CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static7.orstatic.com/userphoto/photo/A/8B4/01N36I8D34B9EA6A565DABpx.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="餐蛋治",
                        display_text="餐蛋治",
                        text="餐蛋治",
                        value="餐蛋治"
                    )
                ],
            )),CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static7.orstatic.com/userphoto/photo/A/8B4/01N36I8D34B9EA6A565DABpx.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="餐蛋治",
                        display_text="餐蛋治",
                        text="餐蛋治",
                        value="餐蛋治"
                    )
                ],
            ))
        ]
class SuggestActionsBot(ActivityHandler):
    uninit = "uninit"
    reserve = "reserve"
    order = "order"
    check = "check"

    context = uninit
    class reservation_profile:
        date_time=None
        num=None

    """
    This bot will respond to the user's input with suggested actions.
    Suggested actions enable your bot to present buttons that the user
    can tap to provide input.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        return await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """
        print("\n turn_context", turn_context.activity)
        text = ''
        if turn_context.activity.text:
            text = turn_context.activity.text.lower()
        else:
            text = turn_context.activity.value
        
        print("\n text", text)
        response_text = self._process_input(text)

        for i in response_text:
            if i == 505:
                await turn_context.send_activity(MessageFactory.text("What else can I do for you?"))
                await self._send_suggested_actions(turn_context)
            else:
                await turn_context.send_activity(i)

        # return await self._send_suggested_actions(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Welcome to 澳洲牛奶公司! I'm SmartServe, your waiter today. How can I help you?"
                    )
                )

                await self._send_suggested_actions(turn_context)

    def _process_input(self, text: str):
        response = []

        if text == reserve:
                self.context = reserve
                response.append(MessageFactory.text("How many people will there be?"))
                return response

        elif text == order:
                self.context = order
                response.append(MessageFactory.carousel(menu,"Here is our menu."))
                return response

        elif text == check:
                self.context = "blue"
                response.append(MessageFactory.text("Here is your bill."))
                return response

        elif self.context == order:
            if text == "餐蛋治":
                response.append(MessageFactory.text("Sure thing! Your order has been placed"))
                response.append(505)
                return response
        elif self.context == reserve:
            if text.isdigit():
                self.reservation_profile.num = text
                response.append(MessageFactory.text("Get it, so what date and time are you booking for?"))
                return response
            else:
                self.reservation_profile.date_time = text
                response.append(MessageFactory.text("All done! A table of "+self.reservation_profile.num+" people is reserved for you on "+self.reservation_profile.date_time+"."))
                response.append(505)
                return response

        response.append(MessageFactory.text("Please select a color from the suggested action choices"))
        return response

    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        reply = MessageFactory.text("")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(title="Reserve a table", type=ActionTypes.im_back, value=reserve),
                CardAction(title=order, type=ActionTypes.im_back, value=order),
                CardAction(title=check, type=ActionTypes.im_back, value=check),
            ]
        )

        return await turn_context.send_activity(reply)
